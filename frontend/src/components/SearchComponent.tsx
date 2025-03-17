import React from 'react';

const SearchComponent: React.FC = () => {
  return (
    <div className="flex items-center">
      <input
        type="text"
        placeholder="Ask anything..."
        className="mr-2 p-2 border border-gray-300 rounded"
      />
    </div>
  );
};

export default SearchComponent;