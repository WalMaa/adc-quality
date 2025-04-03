import { useEffect, useState } from 'react';
import { useParams } from 'react-router';

type ResponseData = {
  _id: string;
  system_message: string;
  user_message: string;
  response: string;
};

export default function ResponsePage() {
  const { id } = useParams();
  const [response, setResponse] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getResponse = async () => {
      try {
        const res = await fetch(`http://localhost:8000/responses/${id}`);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data: ResponseData = await res.json();
        setResponse(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('An unknown error occurred');
        }
      } finally {
        setLoading(false);
      }
    };

    getResponse();
  }, [id]);

  if (loading) {
    return <div className="text-gray-500">Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }

  if (!response) {
    return <div className="text-gray-500">No response data available</div>;
  }

  return (
    <div className="flex justify-center items-center container mx-auto">
      <div className="p-6 rounded-lg shadow-md max-w-xl w-full">
        <h2>System Message:</h2>
        <p>{response.system_message}</p>
        <h2>User Message:</h2>
        <p>{response.user_message}</p>
        <h2>Response:</h2>
        <p>{response.response}</p>
      </div>
    </div>
  );
}