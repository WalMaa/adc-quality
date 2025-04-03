import { render, screen, waitFor } from '@testing-library/react'
import Sidebar from '../components/Sidebar';
import { describe, it, expect, vi, beforeEach } from 'vitest'

export type Response = {
    _id: string;
    system_message: string;
    user_message: string;
    response: string;
};

vi.mock('lucide-react', () => ({
  MessageSquareMore: () => <div data-testid="message-icon" />,
}))

const mockResponses: Response[] = [
  {
    _id: '1',
    system_message: 'You are a helpful assistant',
    user_message: 'How are you?',
    response: 'I am doing well, thank you!',
  },
  {
    _id: '2',
    system_message: 'You are a pirate',
    user_message: 'Where is the treasure?',
    response: 'Arrr, the treasure be buried on the island!',
  },
]

describe('Sidebar Component', () => {
  beforeEach(() => {
    vi.resetAllMocks()

    global.fetch = vi.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockResponses),
        ok: true,
      })
    )
  })

  it('renders the sidebar with "New Prompt" link', async () => {
    render(<Sidebar />)
    
    expect(screen.getByText('New Prompt')).toBeInTheDocument()
    expect(screen.getByTestId('message-icon')).toBeInTheDocument()
  })

  it('fetches and displays responses', async () => {
    render(<Sidebar />)

    await waitFor(() => {
      expect(screen.getByText('How are you?')).toBeInTheDocument()
      expect(screen.getByText('You are a helpful assistant')).toBeInTheDocument()
      expect(screen.getByText('Where is the treasure?')).toBeInTheDocument()
      expect(screen.getByText('You are a pirate')).toBeInTheDocument()
    })
  })

  it('displays correct number of response items', async () => {
    render(<Sidebar />)
    
    await waitFor(() => {
      const items = screen.getAllByRole('link')
      expect(items).toHaveLength(mockResponses.length + 1)
    })
  })

  it('shows correct numbering for response items', async () => {
    render(<Sidebar />)
    
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument()
      expect(screen.getByText('2')).toBeInTheDocument()
    })
  })

  it('handles fetch error gracefully', async () => {
    global.fetch = vi.fn().mockImplementationOnce(() =>
      Promise.reject(new Error('Network error'))
    )
    
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    render(<Sidebar />)
    
    await waitFor(() => {
      expect(screen.getByText('New Prompt')).toBeInTheDocument()
      expect(screen.queryByText('How are you?')).not.toBeInTheDocument()
    })
    
    consoleSpy.mockRestore()
  })

  it('has correct links for each response', async () => {
    render(<Sidebar />)
    
    await waitFor(() => {
      const links = screen.getAllByRole('link')
      expect(links[0]).toHaveAttribute('href', '/')
      expect(links[1]).toHaveAttribute('href', '/responses/1')
      expect(links[2]).toHaveAttribute('href', '/responses/2')
    })
  })

  it('applies correct styling', async () => {
    render(<Sidebar />)
    
    const sidebar = screen.getByRole('complementary')
    expect(sidebar).toHaveClass('fixed')
    expect(sidebar).toHaveClass('w-64')
    expect(sidebar).toHaveClass('border-r')
    
    await waitFor(() => {
      const firstItem = screen.getByText('How are you?').closest('a')
      expect(firstItem).toHaveClass('border-b')
      expect(firstItem).toHaveClass('border-gray-600')
    })
  })

  it('truncates long messages', async () => {
    const longMessage = 'This is a very long message that should be truncated in the sidebar display'
    global.fetch = vi.fn().mockImplementationOnce(() =>
      Promise.resolve({
        json: () => Promise.resolve([{
          _id: '3',
          system_message: 'System message',
          user_message: longMessage,
          response: 'Response',
        }]),
        ok: true,
      })
    )
    
    render(<Sidebar />)
    
    await waitFor(() => {
      const truncatedElement = screen.getByText(longMessage)
      expect(truncatedElement).toHaveClass('truncate')
      expect(truncatedElement.closest('div')).toHaveClass('w-40')
    })
  })
})