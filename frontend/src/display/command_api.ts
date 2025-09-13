import axios from "axios";
import { CommandListResponse } from "../data/response";
import { API_URL } from "../environment"; 

export const getCommands = async (): Promise<CommandListResponse> => {
  try {
    const { data } = await axios.get<CommandListResponse>(`${API_URL}/commands/`)
    return data;
  } catch (error) {
    console.error(`Error getting commands: ${error}`);
    throw error
  }
}

export const deleteCommand = async (id: number): Promise<CommandListResponse> => {
  try {
    await axios.delete<CommandListResponse>(`${API_URL}/commands/${id}`)
    const { data } = await axios.get<CommandListResponse>(`${API_URL}/commands/${id}`)
    return data;
  } catch (error) {
    console.error(`Error deleting command with ID ${id}): ${error}`);
    throw error
  }
}
