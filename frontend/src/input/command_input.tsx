import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { getMainCommands, createCommand } from "./input_api";
import { getCommands } from "../display/command_api";


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
      const data = await getMainCommands(); 
      setMainCommands(data.data);
    };
  
    fetchMainCommands();
  }, []);

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  const commandData = {
    command_type: selectedCommand?.id,
    params: Object.values(parameters).join(",") 
  };
  
  await createCommand(commandData);
  const updatedCommands = await getCommands();
  setCommands(updatedCommands.data);
  setSelectedCommand(null);
  setParameters({});
}

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => {
              const command = mainCommands.find(cmd => cmd.id === Number(e.target.value));
              setSelectedCommand(command || null);
            }}>
              <option value="">Select a command</option>
              {mainCommands.map((command) => (
                <option key={command.id} value={command.id}>
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
