import React, { useEffect, useState } from "react"
import "./command_input.css"
import { MainCommandListResponse, MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"

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
        alert("Could not fetch main commands. Try again.")
      }
    }
    fetchMainCommands();
  }, []);

  const handleCommandChange = (e:React.ChangeEvent<HTMLSelectElement>) => {
    //find() will not work if mainCommands is null
    if (!mainCommands){
      alert("Could not fetch main commands. Try again.")
      return
    }
    const response = mainCommands.data.find((command:MainCommandResponse) => (command.id.toString() === e.target.value));
    if (!response){
      alert("Could not find selected command in main commands.")
      return 
    }
    setSelectedMainCommand(response);
    const newParams: {[key:string]: string} = {};
    response.params?.split(',').forEach((param) => (newParams[param] = ""));
    setCommandParams(newParams);
  }
  const handleParamChange = (param:string, newValue:string) => {
    setCommandParams((prev) => (
      {...prev, [param]:newValue}
    ))
  }

  const handleSubmit = async (e:React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint
     e.preventDefault();
     if (!selectedMainCommand || !commandParams){
      console.error("Error submitting command. Ensure command is selected and params are filled out.");
      return;
     }
     
     const request = {
      name: selectedMainCommand.name,
      params: Object.keys(commandParams).map((param) => commandParams[param]).join(","),
      format: null,
      // command_type IS part of CommandRequest in the backend but NOT the frontend model...is this intentional?
      command_type: selectedMainCommand.id
     };
     console.log(request);
     try {
      const response = await createCommand(request);
      console.log("Command created: ", response);
      setSelectedMainCommand(null);
      setCommandParams(null);
      window.location.reload();
     } catch (error) {
      alert("Could not create command.");
     }
     
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
