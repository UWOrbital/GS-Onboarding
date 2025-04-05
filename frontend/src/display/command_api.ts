import axios from "axios";
import { CommandListResponse } from "../data/response";
import { API_URL } from "../environment";

export const getCommands = async (): Promise<CommandListResponse> => {
  try {
    const { data } = await axios.get<CommandListResponse>(`${API_URL}/commands/`)
    return data;
  } catch (error) {
    console.error(error)
    throw error
  }
}

/**
 * TODO: (Member) Create a deleteCommand API function based on the following specs. You should be using axios to make the API call
 *
 * Deletes the command with the given id on the backend and returns the list of commands after its deletion.
 *
 * @param id: command to delete
 * @returns Promise<CommandListResponse>: list of commands after the command with the given id was deleted
 */

export const deleteCommand = async (id: number): Promise<CommandListResponse> => {
  try {
    //Perform a DELETE request to the API to delete the command by its ID
    const { data } = await axios.delete<CommandListResponse>(`${API_URL}/commands/${id}`);
    return data; // Returns updated list of commands after deletion
  } catch (error) {
    console.error(`Error deleting command with ID ${id}:`, error);
    throw error;
  }
};

export const createCommand = async (commandType: string, params: string): Promise<void> => {
  try {
    await axios.post(`${API_URL}/commands/`, { command_type: commandType, params });
  } catch (error) {
    console.error("Error creating command:", error);
    throw error;
  }
};