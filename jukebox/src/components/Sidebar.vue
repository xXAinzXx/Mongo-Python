<script setup>
import { onMounted, ref, inject } from 'vue';
import { config } from "../service/api.ts";
import { getLocalStorageItems, setLocalStorageItems } from '../service/LocalStorage.ts';
import axios from 'axios';
import LoadingGridPlaylist from "../components/LoadingGridPlaylist.vue";

const { playlists, getPlaylists } = inject('playlists')
const sidebarOpen = ref(true);
const isPlaylistOpen = ref(new Array());
const currentlyPlayedSongUrl = ref("public/songs/a-call-to-the-soul.mp3");
const showPlaylistContainer = ref(false);
const selectedPlaylistId = ref("");
const currentSong = ref();
const loaded = ref(false);

onMounted(async () => {
    await getPlaylists().then(async () => {
        loaded.value = true;
        isPlaylistOpen.value = new Array(playlists.length);

        closeAllPlaylists();
        selectedPlaylistId.value = await getLocalStorageItems("selectedPlaylist");  // must not be converted
        const index = playlists.value.findIndex(x => x._id === selectedPlaylistId.value);
        isPlaylistOpen.value[index] = !isPlaylistOpen.value[index];
    });
})

/**
 * closes all Playlists
 */
function closeAllPlaylists() {
    isPlaylistOpen.value.fill(false);
}

/**
 * closes the other active playlist (if available)
 * opens the selected playlist and saves the id in LocalStorage
 * @param {string} id id of the toggled playlist
 */
async function togglePlaylist(id) {
    // index in array
    const index = playlists.value.findIndex(x => x._id === id);

    // skip if user wants to close active playlist
    if (isPlaylistOpen.value[index] != true) closeAllPlaylists();

    isPlaylistOpen.value[index] = !isPlaylistOpen.value[index];

    // LS: Update LocalStorage entry
    if (await getLocalStorageItems("selectedPlaylist") == id) await setLocalStorageItems("selectedPlaylist", "null");
    else await setLocalStorageItems("selectedPlaylist", id);

    selectedPlaylistId.value = await getLocalStorageItems("selectedPlaylist");
}

/**
 * Updates the currtlyPlayedSong and stats it automaticly 
 * @param {object} song object with url to song mp3 file; if empty -> close player
 */
async function playSong(song) {
    song.url = "http://localhost:5000/files/" + song._id
    showPlaylistContainer.value = false;    // for reload -> disable object and switch song

    // no song, just close Playlist Container
    if (!song || song.url.trim().length === 0) return;
    currentSong.value = song;   // for next song function

    setTimeout(() => {
        showPlaylistContainer.value = true; // enable object
    }, await changeUrl(song.url));
}

/**
 * changes the url link from the song
 * @param {string} url url to song mp3 file 
 */
async function changeUrl(url) {
    currentlyPlayedSongUrl.value = url;
    return true;
}

/**
 * plays the next song in a playlist based on the given current song.
 * @param {object} song 
 */
function playNextSong(song) {
    // selectedPlaylistId.value + 1, because vue v-for start with 1 & convert to int
    let playlist = playlists.value.find(playlist => playlist.id == parseInt(selectedPlaylistId.value) + 1);

    for (let i = 0; i < playlist.songs.length; i++) {
        // find current song
        if (playlist.songs[i].name == song.name) {
            // last song
            if (playlist.songs[i + 1] == null) playSong(null);
            else playSong(playlist.songs[i + 1]);
        }
    }
}

/**
 * selects playlist with id and creates a new song array, without the song and creates a put request
 * reloads the page, to see the changes
 * @param {string} playlistId id of the playlist to remove the song from 
 * @param {string} deleteSongId id of the song, which has to be removed
 */
async function removeSongFromPlaylist(playlistId, deleteSongId) {
    let putRequest = new Array();
    let thisPlaylistObject;

    // select current playlist object
    thisPlaylistObject = playlists.value.find(x => x._id == playlistId);

    // do not delete the parameters
    thisPlaylistObject.songs.forEach((song, index, array) => {
        if (song._id != deleteSongId) putRequest.push(song._id);
    });

    // convert to post-request format
    putRequest = { "name": thisPlaylistObject.name, "songs": putRequest };
    await axios.put(("http://localhost:5000/playlists/" + playlistId), putRequest, config.headers);
    await getPlaylists()
}
</script>

<template>
    <div class="flex min-h-screen">
        <!-- no v-if because songs will -->
        <div class="relative w-screen sm:w-80 bg-gray-800 text-white p-4" :class="{ 'hidden': !sidebarOpen }">
            <div class="flex items-center mb-4">
                <button class="mr-2 text-white hover:text-gray-300" title="Seitenleiste schliessen"
                    @click="sidebarOpen = false">
                    <img src="../assets/arrowRight.svg" alt=">" />
                </button>
                <span class="font-semibold text-2xl">Playlists</span>
                <span class="mx-2 mt-2">
                    <img src="../assets/playlist.svg" alt="" />
                </span>
                <span class="ml-auto">
                    <router-link :to="'manage-playlist/' + 0">
                        <button title="Neue Playlist erstellen" class="text-white">
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 5v14m-7-7h14"></path>
                            </svg>
                        </button>
                    </router-link>
                </span>
            </div>
            <div v-if="loaded">
                <div v-if="playlists.length != 0" v-for="playlist in playlists" :key="playlist._id">
                    <button class="flex items-center justify-between w-full mb-2 focus:outline-none"
                        @click="togglePlaylist(playlist._id)">
                        <span class="truncate text-md font-bold">
                            {{ playlist.name }}
                            <i>
                                {{ isPlaylistOpen[playlists.findIndex(x => x._id === playlist._id)] ? '(ausgewählt)' : '' }}
                            </i>
                        </span>
                        <div class="flex items-center justify-end">
                            <span class="ml-auto mr-2 w-5">
                                <router-link :to="'/delete-playlist/' + playlist._id" title="Playlist löschen">
                                    <img src="../assets/trashcan.svg" alt="D" />
                                </router-link>
                            </span>
                            <span class="ml-auto mr-2 w-5">
                                <router-link :to="'/manage-playlist/' + playlist._id" title="Playlist bearbeiten">
                                    <img src="../assets/pencil.svg" alt="E" />
                                </router-link>
                            </span>
                            <img :class="{ 'rotate-180': isPlaylistOpen[playlists.findIndex(x => x._id === playlist._id)] }"
                                src="../assets/arrowDown.svg" alt=""
                                :title="!isPlaylistOpen[playlists.findIndex(x => x._id === playlist._id)] ? 'Playlist öffnen' : 'Playlist schliessen'" />
                        </div>
                    </button>
                    <div v-show="isPlaylistOpen[playlists.findIndex(x => x._id === playlist._id)]">
                        <div v-for="song in playlist.songs" class="flex items-center mb-2">
                            <span class="truncate flex-grow">> {{ song.name }}</span>
                            <div class="ml-auto flex">
                                <button class="p-1 hover:bg-gray-500 rounded-full" title="Download">
                                    <a :href="song.url" download target="_blank" class="w-full h-full">
                                        <img src="../assets/download.svg" alt="download" />
                                    </a>
                                </button>
                                <button @click="playSong(song)" class="p-1 hover:bg-green-500 rounded-full ml-1"
                                    title="Play">
                                    <img src="../assets/play.svg" alt="play" />
                                </button>
                                <button @click="removeSongFromPlaylist(playlist._id, song._id)"
                                    class="p-1 hover:bg-red-500 rounded-full ml-1" title="Aus Playlist entfernen">
                                    <img src="../assets/trash.svg" alt="trash" />
                                </button>
                            </div>
                        </div>
                        <!-- Add more items here -->
                    </div>
                </div>
                <!-- No Playlists created -->
                <div v-else>
                    <h1 class="text-xl font-semibold"><i>Keine Playlists vorhaden</i></h1>
                </div>

                <!-- Fixed container for currently played songs -->
                <div v-if="showPlaylistContainer" class="fixed bottom-0 left-0 w-80 bg-gray-800 p-4">
                    <div class="text-white">
                        <div class="flex justify-between">
                            <span class="text-xl font-semibold">Laufendes Lied:</span>
                            <button @click="showPlaylistContainer = false" class="p-2 hover:bg-red-500 rounded-full"
                                title="Song stoppen">
                                <img src="../assets/trash.svg" alt="trash" />
                            </button>
                        </div>
                        <span>{{ currentSong.name }}</span>
                        <ul class="mt-2">
                            <audio @ended="playNextSong(currentSong)" controls autoplay="true">
                                <source :src="currentlyPlayedSongUrl" type="audio/mpeg" />
                                Your browser does not support the audio player.
                            </audio>
                        </ul>
                    </div>
                </div>
            </div>
            <div v-else>
                <LoadingGridPlaylist />
            </div>
        </div>
        <div v-if="!sidebarOpen" class="flex-grow bg-gray-800">
            <button class="mr-2 text-white hover:text-gray-300 p-2" title="Seitenleiste öffnen" @click="sidebarOpen = true">
                <img src="../assets/arrowRight.svg" alt=">" class="w-8 p-1 rotate-180 hover:bg-gray-500 rounded-full" />
            </button>
        </div>
    </div>
</template>

<style scoped></style>