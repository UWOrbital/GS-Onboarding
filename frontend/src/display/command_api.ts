import axios from "axios";
import { CommandListReponse } from "../data/response";
import { API_URL } from "../environment";

export const getCommands = async (): Promise<CommandListReponse> => {
  try {
    const { data } = await axios.get<CommandListReponse>(`${API_URL}/commands/`)
    return data;
  } catch (error) {
    console.error(error)
    throw error
  }
}
