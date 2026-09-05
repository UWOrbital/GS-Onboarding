import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { getMainCommands, createCommand } from "../input/input_api"

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
      const response = await getMainCommands();
      setMainCommands(response.data)
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
    e.preventDefault()
    if (selectedCommand === null) {
      return;
    }

    const requestData = {
      command_type: selectedCommand.id,
      params: selectedCommand?.params ? selectedCommand.params.split(",").map(name => parameters[name]).join(",") : null
    }

    const response = await createCommand(requestData);
    setCommands((prev) => [...prev, response.data]);
  }

  const handleCommandChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const commandId = parseInt(e.target.value);
    const command = mainCommands.find((cmd) => cmd.id === commandId) || null;
    setSelectedCommand(command);
    setParameters({});
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={handleCommandChange}>{/* TODO: (Member) Display the list of commands based on the get commands request.
                        It should update the `selectedCommand` field when selecting one.*/}
              {mainCommands.map((cmd) => (
                <option key={cmd.id} value={cmd.id}>
                  {cmd.name}
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
