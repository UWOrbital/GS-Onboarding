import { useEffect, useState } from "react"
import { CommandResponse } from "../data/response"
import { getCommands } from "./command_api"
import CommandRow from "./row"

const CommandTable = () => {
  const [commands, setCommands] = useState<CommandResponse[]>([])

  const getCommandsFn = async () => {
    const data = await getCommands();
    setCommands(data.data)
  }

  useEffect(() => {
    getCommandsFn();
  }, [])

  const handleDelete = (id: number) => {
    return () => {
      // TODO: (Member) Handle delete logic here

    }
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID: </th>
          <th>Name: </th>
          <th>Params: </th>
          <th>Format: </th>
          <th>Created On: </th>
          <th>Updated On: </th>
          <th>Delete</th>
        </tr>
      </thead>
      <thead>
        {commands.map(value => (<CommandRow {...value} handleDelete={handleDelete(value.id)} />))}
      </thead>
    </table>
  )
}

export default CommandTable;
