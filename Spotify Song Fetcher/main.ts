import axios from "axios";
import * as dotenv from "dotenv";
dotenv.config();
import playlists from "./data/playlists.json";
import { Playlist } from "./types";

const SPOTIFY_TOKEN_ENDPOINT: string = process.env.SPOTIFY_TOKEN_ENDPOINT as string;
const SPOTIFY_CLIENT_ID: string = process.env.SPOTIFY_CLIENT_ID as string;
const SPOTIFY_CLIENT_SECRET: string = process.env.SPOTIFY_CLIENT_SECRET as string;

const grabToken = async (clientId: string, clientSecret: string): Promise<string> => {
  const endpoint = "https://accounts.spotify.com/api/token";

  // I was going to make a decorator for this but it might be better to allow each function to granularly handle errors
  try {
    const response = await axios.post(
      endpoint,
      {
        grant_type: "client_credentials",
        client_id: clientId,
        client_secret: clientSecret,
      },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    // we only care about the access_token
    return response.data.access_token;
  } catch (error: any) {
    throw new Error(`An error has occurred during ${grabToken.name}(): ${error}`);
  }
};

const getArtist = async (token: string, artistId: string) => {
  const endpoint = `https://api.spotify.com/v1/artists/${artistId}`;

  try {
    const response = await axios.get(endpoint, {
      headers: {
        Authorization: `Bearer  ${token}`,
      },
    });

    return response;
  } catch (error) {
    throw new Error(`An error has occurred during ${getArtist.name}(): ${error}`);
  }
};

const getPlaylistItems = async (
  token: string,
  playlistId: string = "37i9dQZF1DZ06evO1JPXRC",
  market?: string,
  fields?: string,
  limit?: Number,
  offset?: Number,
  additonalTypes?: string
) => {
  // I need to build some type of query string builder for the optional args

  const endpoint = `https://api.spotify.com/v1/playlists/${playlistId}/tracks`;

  try {
    const response = await axios.get(endpoint, {
      headers: {
        Authorization: `Bearer  ${token}`,
      },
    });

    return response.data.items;
  } catch (error) {
    throw new Error(`An error has occurred during ${getPlaylistItems.name}(): ${error}`);
  }
};

const getTopPlaylistsByYear = async (token: string, playlists: Playlist[]) => {
  // iterates through a playlists.json and grabs each playlist object

  return Promise.all(playlists.map(async (playlist) => await getPlaylistItems(token, playlist.playlistId)));
};

const run = (async () => {
  const token = await grabToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET);
  getTopPlaylistsByYear(token, playlists).then((data) => console.log(data));
})();
