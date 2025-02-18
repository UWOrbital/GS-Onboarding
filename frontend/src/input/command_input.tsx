import React, { ReactElement, useEffect, useState } from "react"
import "./command_input.css"
import { MainCommandListResponse, MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"
import { CommandRequest } from "../data/request"


const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [mainCommands, setMainCommands] = useState<MainCommandListResponse|null>(null);
  const [selectedMainCommand, setSelectedMainCommand] = useState<MainCommandResponse|null>(null);
  const [ commandParams, setCommandParams ] = useState<{[key:string]: string}|null>(null);
  
  useEffect(() => {
    const fetchMainCommands = async() => {
      try {
        const response:MainCommandListResponse = await getMainCommands();
        setMainCommands(response);
      } catch (error) {
        console.error("Error fetching main commands: ", error);
        throw error;
      }
    }
    fetchMainCommands();
  }, []);

  const handleCommandChange = (e:React.ChangeEvent<HTMLSelectElement>) => {
    //find() will not work if mainCommands is null
    if (mainCommands){
      const response = mainCommands.data.find((command:MainCommandResponse) => (command.id.toString() === e.target.value));
      //response could be null if not found
      if (response) {
        setSelectedMainCommand(response);
        const newParams: {[key:string]: string} = {};
        response.params?.split(',').forEach((param) => (newParams[param] = ""));
        setCommandParams(newParams);
      }
    }
  }
  const handleParamChange = (param:string, newValue:string) => {
    setCommandParams((prev) => (
      {...prev, [param]:newValue}
    ))
  }

  const handleSubmit = async (e:React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint
     
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={handleCommandChange}>
              {mainCommands && mainCommands.data.map((command) => (
                <option value={command.id}>{command.name}</option>
              ))}
            </select>
          </div>  
          {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          {selectedMainCommand && commandParams && Object.keys(commandParams).map((key:string) => (<input placeholder={key} value={commandParams[key]} onChange={(e) => handleParamChange(key, e.target.value)}/>))}
          <button type="submit">Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
