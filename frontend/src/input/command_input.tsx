import "./command_input.css"
import { useState, useEffect } from "react"
import { MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"


const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [commandType, setCommandType] = useState<string>("1")
  const [params, setParams] = useState<string>("")
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([])

  
  useEffect(() => {
    const setMainCommandsFn = async () => {
      const data = await getMainCommands()
      setMainCommands(data.data)
    }

    setMainCommandsFn();
  }, [])
  

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    // TODO:(Member) Submit to your post endpoint
    e.preventDefault();
    const reqBody = {
      command_type: +commandType,
      params: params,
    };

    //console.log('Req body:', reqBody);

    const createCommandFn = async () => {
      await createCommand(reqBody);
    }

    createCommandFn();
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select value={commandType} onChange={(e) => setCommandType(e.target.value)}>{/* TODO: (Member) Display the list of commands based on the get commands request*/}
              {mainCommands.map(cmd => (<option value={cmd.id}>{cmd.name}</option>))}
            </select>
          </div>
          <input value={params} onChange={(e) => setParams(e.target.value)}/> {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          <button type="submit">Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
