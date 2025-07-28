import { useEffect, useState } from 'react'
import './app.css'
import CommandTable from './display/table'
import CommandInput from './input/command_input'
import { CommandResponse } from './data/response'
import { getCommands } from './display/command_api'

function App() {
  const [commands, setCommands] = useState<CommandResponse[]>([])

  useEffect(() => {
    const getCommandsFn = async () => {
      try {
        const data = await getCommands();
        setCommands(data.data)
      } catch (error) {
        console.error(error)
        alert("Error fetching commands")
      }
    }

    getCommandsFn();
  }, [])

  return (
    <>
      <CommandInput setCommands={setCommands} />
      <p>Command List:</p>
      <CommandTable commands={commands} setCommands={setCommands} />
    </>
  )
}

export default App
