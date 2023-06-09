from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from src.models.Playlist import Playlist, PlaylistCreate, PlaylistUpdate
from src.models.Song import Song

router = APIRouter()

@router.get("/", response_description="get list of songs", status_code=status.HTTP_200_OK, response_model=List[Playlist])
def get_playlists(request: Request):
    playlists = request.app.MongoDb.getPlaylists()
    return playlists

@router.get("/{id}", response_description="get list of songs", status_code=status.HTTP_200_OK, response_model=Playlist)
def get_playlist(id: str, request: Request):
    playlists = request.app.MongoDb.findPlaylistById(id)
    return playlists

@router.get("/{id}/songs", response_description="get list of songs", status_code=status.HTTP_200_OK, response_model=List[Song])
def get_songsFromPlaylist(id: str, request: Request):
    songs = request.app.MongoDb.getSongsFromPlaylist(id)
    return songs

@router.delete("/{id}", response_description="delete song", status_code=status.HTTP_200_OK, response_model=Playlist)
def delete_playlist(id: str, request: Request):
    result = request.app.MongoDb.deletePlaylist(id)
    return {"Deleted": result.deleted_count}

@router.post("/", response_description="Create a new song", status_code=status.HTTP_201_CREATED, response_model=PlaylistCreate)
def create_playlist(request: Request, playlists: Playlist = Body(...)):
    playlists = jsonable_encoder(playlists)
    new_playlists = request.app.MongoDb.InsertPlaylist(playlists)
    created_playlists = request.app.MongoDb.findPlaylistById(new_playlists.inserted_id)
    return created_playlists

@router.put("/{id}", response_description="Edit a song", status_code=status.HTTP_201_CREATED, response_model=PlaylistUpdate)
def update_playlist(id: str, request: Request, playlist: PlaylistUpdate = Body(...)):
    playlist = {k: v for k, v in playlist.dict().items() if v is not None}
    if len(playlist) >= 1:
        update_result = request.app.MongoDb.UpdatePlaylist(id, playlist) 
    if (
        existing_playlist := request.app.MongoDb.playlistCollection.find_one({"_id": id})
    ) is not None:
        return existing_playlist  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {id} not found")