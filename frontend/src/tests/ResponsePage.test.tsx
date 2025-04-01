import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import ResponsePage from '../ResponsePage';
import { useParams } from 'react-router';

// Mock the fetch API and react-router
vi.mock('react-router', () => ({
  useParams: vi.fn(),
}));

const mockResponse = {
  _id: '123',
  system_message: 'Test system message',
  user_message: 'Test user message',
  response: 'Test response content'
};

describe('ResponsePage Component', () => {
  beforeEach(() => {
    // Clear all mocks between tests
    vi.clearAllMocks();
    
    // Setup default mock for useParams
    vi.mocked(useParams).mockReturnValue({ id: '123' });
    
    // Setup proper fetch mock with Response-like object
    global.fetch = vi.fn(() => 
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
        json: () => Promise.resolve(mockResponse),
      } as Response)
    );
  });

  it('displays loading state initially', () => {
    render(<ResponsePage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    expect(screen.getByText('Loading...')).toHaveClass('text-gray-500');
  });

  it('fetches and displays response data', async () => {
    render(<ResponsePage />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/responses/123');
    });

    expect(screen.getByText('System Message:')).toBeInTheDocument();
    expect(screen.getByText(mockResponse.system_message)).toBeInTheDocument();
    expect(screen.getByText('User Message:')).toBeInTheDocument();
    expect(screen.getByText(mockResponse.user_message)).toBeInTheDocument();
    expect(screen.getByText('Response:')).toBeInTheDocument();
    expect(screen.getByText(mockResponse.response)).toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('API Error')));
  
    render(<ResponsePage />);
  
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/responses/123');
    });
  
    // Check for the error message
    await waitFor(() => {
      expect(screen.getByText('Error: API Error')).toBeInTheDocument();
    });
  });

  it('applies correct styling', async () => {
    render(<ResponsePage />);

    await waitFor(() => {
      expect(screen.getByText(mockResponse.system_message)).toBeInTheDocument();
    });

    const container = screen.getByText('System Message:').closest('div.flex');
    expect(container).toBeInTheDocument();
    expect(container).toHaveClass('justify-center', 'items-center', 'container', 'mx-auto');
    
    // Get the content card
    const contentCard = screen.getByText('System Message:').closest('div.p-6');
    expect(contentCard).toBeInTheDocument();
    expect(contentCard).toHaveClass('rounded-lg', 'shadow-md', 'max-w-xl', 'w-full');
  });
});