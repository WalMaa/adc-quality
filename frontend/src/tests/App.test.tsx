import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'
import { describe, it, expect, vi, beforeEach } from 'vitest'


vi.mock('lucide-react', () => ({
    Loader2: () => <span data-testid="loader-icon">Loading...</span>,
  }))

global.fetch = vi.fn()

describe('App Component', () => {
  const mockLLMs = {
    llms: [{ name: 'llm1' }, { name: 'llm2' }],
    selected_llm: 'llm1'
  }

  const mockPromptResponse = {
    response: {
      content: 'Test response content'
    }
  }

  beforeEach(() => {
    vi.clearAllMocks()
    
    // Mock the initial API calls
    global.fetch = vi.fn()
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve(mockLLMs),
          ok: true
        })
      )
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve({ selected_llm: 'llm1' }),
          ok: true
        })
      )
  })

  it('renders correctly with initial state', async () => {
    render(<App />)
    
    expect(screen.getByDisplayValue('you are a pirate')).toBeInTheDocument()
    expect(screen.getByDisplayValue('what is 1+1')).toBeInTheDocument()
    expect(screen.getByText('Submit')).toBeInTheDocument()
    expect(screen.getByText('Output:')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('llm1')).toBeInTheDocument()
    })
  })

  it('handles prompt submission successfully', async () => {
    global.fetch = vi.fn()
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve(mockLLMs),
          ok: true
        })
      )
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve({ selected_llm: 'llm1' }),
          ok: true
        })
      )
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve(mockPromptResponse),
          ok: true
        })
      )

    render(<App />)
    
    await userEvent.click(screen.getByText('Submit'))
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          system_message: 'you are a pirate',
          user_message: 'what is 1+1',
        }),
      })
      expect(screen.getByText('Test response content')).toBeInTheDocument()
    })
  })

  it('updates system text when changed', async () => {
    render(<App />)
    
    const systemInput = screen.getByDisplayValue('you are a pirate')
    await userEvent.clear(systemInput)
    await userEvent.type(systemInput, 'new system text')
    
    expect(systemInput).toHaveValue('new system text')
  })

  it('updates user message when changed', async () => {
    render(<App />)
    
    const userInput = screen.getByDisplayValue('what is 1+1')
    await userEvent.clear(userInput)
    await userEvent.type(userInput, 'new user message')
    
    expect(userInput).toHaveValue('new user message')
  })

  it('shows loading state during submission', async () => {
    let resolvePromise: (value: any) => void
    const promise = new Promise(resolve => {
      resolvePromise = resolve
    })
    
    global.fetch = vi.fn()
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve(mockLLMs),
          ok: true
        })
      )
      .mockImplementationOnce(() => 
        Promise.resolve({
          json: () => Promise.resolve({ selected_llm: 'llm1' }),
          ok: true
        })
      )
      .mockImplementationOnce(() => promise)

    render(<App />)
    
    const submitBtn = screen.getByRole('button', { name: /submit/i })
    await userEvent.click(submitBtn)
    
    await waitFor(() => {
      expect(submitBtn).toBeDisabled()
      expect(screen.getByTestId('loader-icon')).toBeInTheDocument()
    })
    
    // Resolve the promise
    resolvePromise!({
      json: () => Promise.resolve(mockPromptResponse),
      ok: true
    })
    
    await waitFor(() => {
      expect(submitBtn).not.toBeDisabled()
      expect(screen.queryByTestId('loader-icon')).not.toBeInTheDocument()
    });
});
});