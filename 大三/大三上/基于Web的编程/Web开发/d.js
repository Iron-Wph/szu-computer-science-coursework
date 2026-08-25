import React, { useState } from 'react';

function App() {
    const content = "默认内容";

  function handleClick() {
    content = "新内容";
  }

  return (
    <div>
      <p>{content}</p>
      <button onClick={handleClick}>按钮</button>
    </div>
  );
}

export default App;
