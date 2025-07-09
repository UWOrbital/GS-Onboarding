import { CommandResponse } from "../data/response"
import CommandRow from "./row"

interface CommandTableProp {
  commands: CommandResponse[],
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandTable = ({
  commands,
  setCommands // Used by handleDelete to update commands
}: CommandTableProp) => {

  const handleDelete = (id: number) => {
    return () => {
      // TODO: (Member) Handle delete logic here
      // You will need to create a function in `command_api.ts` before you can finish this part.

    }
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID: </th>
          <th>Main Command ID: </th>
          <th>Params: </th>
          <th>Status: </th>
          <th>Created On: </th>
          <th>Updated On: </th>
          <th>Delete</th>
        </tr>
      </thead>
      <thead>
        {commands.map(value => (<CommandRow key={value.id} {...value} handleDelete={handleDelete(value.id)} />))}
      </thead>
    </table>
  )
}

export default CommandTable;
