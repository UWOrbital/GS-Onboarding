import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse} from "../data/response"
import "./command_input.css"
import { MainCommandListResponse } from "../data/response";
import axios from "axios";
import { API_URL } from "../environment"; 
import { getMainCommands } from "./input_api"
import { CommandRequest } from "../data/request";

interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  const [mainCommands, setMainCommands] = useState<MainCommandListResponse | null>(null);

  useEffect(() => {
    const fetchCommands = async() => {
      const data = await getMainCommands();
      setMainCommands(data);
    };
    fetchCommands();
  }, []);

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (mainCommands == null) return;
    const selectedID = e.target.value;
    const command = mainCommands.data.find(c => c.id === Number(selectedID));
    setSelectedCommand(command ?? null)
  } 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCommand) {
      console.error(`Exited early`);
      return;
    }
    const payload: CommandRequest = {
      command_type: selectedCommand.id,
      params: selectedCommand.params
    }
    const response = await axios.post(`${API_URL}/commands/`, payload);
    const newCommand: CommandResponse = response.data;
    setCommands(prev => [...prev, newCommand]);
  }
 
  if (mainCommands) return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            
            <select value={selectedCommand ? selectedCommand.id : ""} onChange={handleChange}

            >{/* TODO: (Member) Display the list of commands based on the get commands request.
                        It should update the `selectedCommand` field when selecting one.*/}
              {/* <option value={"1"}>Command 1</option>
              <option value={"2"}>Command 2</option>
              <option value={"3"}>Command 3</option> */}

              {mainCommands?.data.map(command => (
                <option value={command.id}>
                  {command.name}
                </option>
              ))}
            </select>
          </div>
          {selectedCommand?.params?.split(",").map((param) => (
            <div key={param}>
              <label htmlFor={`param-${param}`}>{param}: </label>
              <input
                id={`param-${param}`}
                type="text"
                value={parameters[param] || ""}
                onChange={(e) => handleParameterChange(param, e.target.value)}
                placeholder={`Enter ${param}`}
              />
            </div>
          ))}
          <button type="submit">Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
