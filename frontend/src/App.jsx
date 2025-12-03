import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import GoalChatPage from './pages/GoalChatPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Landing />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/register' element={<RegisterPage />} />
        <Route path='/setup1' element={<GoalChatPage />} />
      </Routes>
    </BrowserRouter>
  )
}