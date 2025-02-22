import { API_URL } from "../environment";
import { CommandRequest } from "../data/request";
import axios from "axios";
import { CommandResponse, MainCommandListResponse } from "../data/response";

export const createCommand = async (requestData: CommandRequest): Promise<CommandResponse> => {
  try {
    const { data } = await axios.post<CommandResponse>(`${API_URL}/commands`, requestData);
    return data
  } catch (error) {
    console.error("Error creating command: ", error);
    throw error;
  }
}

export const getMainCommands = async (): Promise<MainCommandListResponse> => {
  try {
    const { data } = await axios.get<MainCommandListResponse>(`${API_URL}/main-commands/`);
    return data;
  } catch (error) {
    console.error("Error fetching commands: ", error);
    throw error;
  }
}
