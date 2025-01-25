import './app.css'
import CommandTable from './display/table'
import CommandInput from './input/command_input'

function App() {
  return (
    <>
      <CommandInput />
      <p>Command List:</p>
      <CommandTable />
    </>
  )
}

export default App
