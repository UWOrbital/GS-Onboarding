import { API_URL } from "../environment";
import { CommandRequest, CommandResponse } from "../data/command";
import axios from "axios";

export const createCommand = async (requestData: CommandRequest): Promise<CommandResponse | undefined> => {
  try {
    const { data } = await axios.post<CommandResponse>(`${API_URL}/commands`, requestData);
    return data
  } catch (error) {
    console.error(error);
  }
}
