import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { getMainCommands, createCommand } from "./input_api";


interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  const [commands, setCommandsList] = useState<MainCommandResponse[]>([]);

  useEffect(() => {
  const fetchCommands = async () => {
    try {
      const response = await getMainCommands();
      setCommandsList(response.data);
    } catch (error) {
      console.error('Error fetching commands:', error);
    }
  };
  fetchCommands();
}, []);

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); 
    if (!selectedCommand) return;
    try {
      const newCommand = await createCommand({
        command_type: selectedCommand.id,
        params: Object.values(parameters).join(",") || null
      });
      setCommands(prev => [...prev, newCommand.data]); 
      setSelectedCommand(null);
      setParameters({});
    } catch (error) {
      console.error("Error creating command:", error);
    }
};
    
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select 
              value={selectedCommand?.id || ""}
              onChange={(e) => {
                const cmd = commands.find(c => c.id === Number(e.target.value));
                setSelectedCommand(cmd || null);
                setParameters({});
              }}
            >
              <option value="">Select a command...</option>
              {commands.map(cmd => (
                <option key={cmd.id} value={cmd.id}>{cmd.name}</option>
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
          <button type="submit" disabled={!selectedCommand}>Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;