import { useEffect, useState } from "react";
import { CommandResponse } from "../data/response";
import { getCommands, deleteCommand } from "./command_api";

import CommandRow from "./row";

const CommandTable = () => {
  const [commands, setCommands] = useState<CommandResponse[]>([]);

  useEffect(() => {
    const getCommandsFn = async () => {
      try {
        const data = await getCommands();
        setCommands(data.data);
      } catch (error) {
        alert("Failed to retrieve commands");
      }
    };

    getCommandsFn();
  }, []);

  const handleDelete = (id: number) => {
    return async () => {
      try {
        await deleteCommand(id);
        window.location.reload();
      } catch (error) {
        alert(`Failed to delete command with id ${id}`);
      }

    };
  };

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
        {commands.map((value) => (
          <CommandRow {...value} handleDelete={handleDelete(value.id)} />
        ))}
      </thead>
    </table>
  );
};

export default CommandTable;
