import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import axios from 'axios'
import App from '../../frontend/src/app'
import { deleteCommand } from '../../frontend/src/display/command_api'
import type { MainCommandResponse, CommandResponse } from '../../frontend/src/data/response'

vi.mock('axios')

const mockMainCommands: MainCommandResponse[] = [
  { id: 1, name: "Main Command 1", params: "time", format: "int 7 bytes", data_size: 7, total_size: 7 },
  { id: 2, name: "Main Command 2", params: "mode_state_number,time", format: "int 1 byte, int 7 bytes", data_size: 8, total_size: 8 },
]

const makeCommand = (overrides: Partial<CommandResponse> & { id: number; command_type: number }): CommandResponse => ({
  status: 1,
  params: null,
  created_on: "2025-01-01T00:00:00Z",
  updated_on: "2025-01-01T00:00:00Z",
  ...overrides,
})

const command1: CommandResponse = makeCommand({ id: 1, command_type: 1, params: "time: 10" })

function setupGetMocks(commands: CommandResponse[] = []) {
  ;(axios.get as Mock).mockImplementation((url: string) => {
    if (url.includes('/main-commands')) {
      return Promise.resolve({ data: { data: mockMainCommands } })
    }
    if (url.includes('/commands')) {
      return Promise.resolve({ data: { data: commands } })
    }
    return Promise.reject(new Error(`Unexpected GET: ${url}`))
  })
}

describe('Frontend Tests', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('deleteCommand API function should use axios.delete', async () => {
    ;(axios.delete as Mock).mockResolvedValueOnce({ data: { data: [] } })
    ;(axios.get as Mock).mockResolvedValueOnce({ data: { data: [] } })

    await deleteCommand(1)

    expect(axios.delete).toHaveBeenCalledTimes(1)
    const callUrl = (axios.delete as Mock).mock.calls[0][0] as string
    expect(callUrl).toMatch(/\/commands\/.*1/)
  })

  it('should load main commands from the backend and display them for selection', async () => {
    setupGetMocks([])
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Main Command 1')).toBeInTheDocument()
      expect(screen.getByText('Main Command 2')).toBeInTheDocument()
    })

    expect(screen.getByRole('combobox')).toBeInTheDocument()
  })

  it('should create a command through the form and display it', async () => {
    const user = userEvent.setup()
    setupGetMocks([])

    ;(axios.post as Mock).mockResolvedValueOnce({
      data: { data: command1 },
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Main Command 1')).toBeInTheDocument()
    })

    // Select Main Command 1 from the dropdown
    const select = screen.getByRole('combobox')
    await user.selectOptions(select, screen.getByRole('option', { name: 'Main Command 1' }))

    // Wait for parameter input(s) to appear and fill them
    await waitFor(() => {
      expect(screen.getAllByRole('textbox').length).toBeGreaterThan(0)
    })
    const inputs = screen.getAllByRole('textbox')
    for (const input of inputs) {
      await user.type(input, '10')
    }

    // Submit the form
    await user.click(screen.getByRole('button', { name: /Submit/i }))

    // Verify the command was created via the API
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledTimes(1)
    })

    // Verify created command data appears on the page
    await waitFor(() => {
      expect(screen.getByText(/time: 10/)).toBeInTheDocument()
    })
  })

  it('should show parameter inputs based on the selected main command', async () => {
    const user = userEvent.setup()
    setupGetMocks([])

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Main Command 2')).toBeInTheDocument()
    })

    // Select Main Command 2 which has two parameters (mode_state_number, time)
    const select = screen.getByRole('combobox')
    await user.selectOptions(select, screen.getByRole('option', { name: 'Main Command 2' }))

    // Should show two input fields for the two parameters
    await waitFor(() => {
      expect(screen.getAllByRole('textbox').length).toBe(2)
    })
  })

  it('should delete a command from the table via the backend', async () => {
    const user = userEvent.setup()

    // Support both re-fetch-after-delete and direct-delete-response patterns
    let commandsGetCount = 0
    ;(axios.get as Mock).mockImplementation((url: string) => {
      if (url.includes('/main-commands')) {
        return Promise.resolve({ data: { data: mockMainCommands } })
      }
      if (url.includes('/commands')) {
        commandsGetCount++
        return Promise.resolve({
          data: { data: commandsGetCount <= 1 ? [command1] : [] }
        })
      }
      return Promise.reject(new Error(`Unexpected GET: ${url}`))
    })
    ;(axios.delete as Mock).mockResolvedValueOnce({ data: { data: [] } })

    render(<App />)

    // Wait for the command to appear
    await waitFor(() => {
      expect(screen.getByText(/time: 10/)).toBeInTheDocument()
    })

    // Find and click a delete button
    const deleteButton = screen.getAllByRole('button').find(
      btn => btn.textContent?.toLowerCase().includes('delete')
    )
    expect(deleteButton).toBeDefined()
    await user.click(deleteButton!)

    // Verify the delete API was called
    await waitFor(() => {
      expect(axios.delete).toHaveBeenCalledTimes(1)
    })

    // Verify the command is removed from the page
    await waitFor(() => {
      expect(screen.queryByText(/time: 10/)).not.toBeInTheDocument()
    })
  })
})
