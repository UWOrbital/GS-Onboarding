import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { getCommands } from "../display/command_api";
import { createCommand, getMainCommands } from "./input_api";
import axios from "axios";
import { API_URL } from "../environment";

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
    const fetchCommands = async () => {
      try {
        const data = await getMainCommands();  
        setMainCommands(data.data); 
      } catch(err) {
        console.log("error fetching stuff"); 
        throw err; 
      }
      
    }

    fetchCommands(); 
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

    if (!selectedCommand) {
      console.log("no value"); 
      return; 
    }

    const payload = {
      ...selectedCommand
    }

    try {
      await createCommand(payload); 
      console.log("submitted successfully"); 
    } catch(err) {
      console.log("failed"); 
      throw err; 
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => {setSelectedCommand(e.target.value)}}>{/* TODO: (Member) Display the list of commands based on the get commands request.
                        It should update the `selectedCommand` field when selecting one.*/}
              {mainCommands.map((cmd) => (
                <option key={cmd.id} value={cmd.id}>
                  {cmd.name}
                </option>))
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
