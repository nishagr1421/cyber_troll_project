import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import ToxicityBadge from './ToxicityBadge'

const API_URL = 'http://localhost:8000'

function CommentComposer({ postId, onCommentAdd }) {
  const [text, setText] = useState('')
  const [toxicityScore, setToxicityScore] = useState(0)
  const [topTokens, setTopTokens] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const debounceTimer = useRef(null)

  useEffect(() => {
    // Debounce API calls
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    if (text.trim().length > 0) {
      setIsTyping(true)
      debounceTimer.current = setTimeout(async () => {
        try {
          const response = await axios.post(`${API_URL}/api/comment/predict`, {
            text: text
          })
          setToxicityScore(response.data.score || 0)
          setTopTokens(response.data.top_tokens || [])
        } catch (error) {
          console.error('Error predicting toxicity:', error)
        } finally {
          setIsTyping(false)
        }
      }, 500) // 500ms debounce
    } else {
      setToxicityScore(0)
      setTopTokens([])
      setIsTyping(false)
    }

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [text])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (text.trim()) {
      await onCommentAdd(postId, text.trim())
      setText('')
      setToxicityScore(0)
      setTopTokens([])
    }
  }

  return (
    <div className="px-4 py-2 border-t border-gray-200">
      <form onSubmit={handleSubmit} className="space-y-2">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Add a comment..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
          <button
            type="submit"
            disabled={!text.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm"
          >
            Post
          </button>
        </div>
        
        {/* Live Toxicity Preview */}
        {text.trim() && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-600">Toxicity:</span>
            {isTyping ? (
              <span className="text-gray-400">Analyzing...</span>
            ) : (
              <>
                <ToxicityBadge score={toxicityScore} />
                {topTokens.length > 0 && (
                  <span className="text-gray-500">
                    Flagged: {topTokens.slice(0, 3).join(', ')}
                  </span>
                )}
              </>
            )}
          </div>
        )}
      </form>
    </div>
  )
}

export default CommentComposer

