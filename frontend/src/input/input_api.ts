import { API_URL } from "../environment";
import { CommandRequest } from "../data/request";
import axios from "axios";
import { CommandResponse, MainCommandListResponse } from "../data/response";

export const createCommand = async (requestData: CommandRequest): Promise<CommandResponse | undefined> => {
  try {
    const { data } = await axios.post<CommandResponse>(`${API_URL}/commands`, requestData);
    return data
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export const getMainCommands = async (): Promise<MainCommandListResponse> => {
  try {
    const { data } = await axios.get<MainCommandListResponse>(`${API_URL}/main-commands/`);
    console.log(data)
    return data;
  } catch (error) {
    console.error(error)
    throw error;
  }
}
