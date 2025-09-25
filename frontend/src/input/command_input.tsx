import { useEffect, useState } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { getMainCommands } from "./input_api";
import { API_URL } from "../environment";
import axios from "axios";

interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  // TODO: (Member) Setup anymore states if necessary
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([]);

  // TODO: (Member) Fetch MainCommands in a useEffect
  useEffect(() => {
    const fetchMainCommands = async () => {
      try {
        const data = await getMainCommands();
        setMainCommands(data.data);
      } catch (error) {
        console.log(`Error fetching MainCommands: ${error}`);
        throw error
      }
    }
    
    fetchMainCommands();
  }, [])

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleSubmit = async (e: React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint 
    e.preventDefault();

    if (selectedCommand) {
      try {
        const command = ({command_type: selectedCommand.id, params: selectedCommand.params});
        const res = await axios.post(`${API_URL}/commands/`, command);
        const newCommand = res.data;
        setCommands(prev => [...prev, newCommand]);
      } catch (error) {
        console.log(`error ${error}`);
        throw error
      }
    } else {
      console.log("no MainCommand selected");
    }
  }

  const handleChangeCommandType = (id: Number) => {
    if (mainCommands) {
      const command = mainCommands.find(command => command.id == id);
      setSelectedCommand(command ? command : null);
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => handleChangeCommandType(Number(e.target.value))}> 
              {/* TODO: (Member) Display the list of commands based on the get commands request.
                        It should update the `selectedCommand` field when selecting one.*/}
              {
                mainCommands.map((command) => (
                  <option key = {command.id} value={command.id}>{command.name}</option>
                ))
              }
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
