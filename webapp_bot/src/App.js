import logo from './logo.svg'
import './App.css'
import { useEffect } from 'react'

const webApp = window.Telegram.WebApp

export default function App() {

  useEffect(() => {
    webApp.ready()
  }, [])

  const onClose = () => {
    webApp.close()
  }

  return (
    <div className="App">
      <header className="App-header">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
      </header>
      <body>
        <button onClick={onClose}>Закрыть</button>
      </body>
    </div>
  );
}
