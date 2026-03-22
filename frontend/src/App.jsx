import { useState, useEffect } from 'react'
import Feed from './components/Feed'
import AdminPanel from './components/AdminPanel'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('feed')

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">InstaGuard</h1>
          <nav className="flex gap-4">
            <button
              onClick={() => setActiveTab('feed')}
              className={`px-4 py-2 rounded-md ${
                activeTab === 'feed'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Feed
            </button>
            <button
              onClick={() => setActiveTab('admin')}
              className={`px-4 py-2 rounded-md ${
                activeTab === 'admin'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Admin
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-6">
        {activeTab === 'feed' ? <Feed /> : <AdminPanel />}
      </main>
    </div>
  )
}

export default App

