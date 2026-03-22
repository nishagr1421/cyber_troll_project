import { useState, useEffect } from 'react'
import axios from 'axios'
import ToxicityBadge from './ToxicityBadge'

const API_URL = 'http://localhost:8000'

function AdminPanel() {
  const [feed, setFeed] = useState([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState('toxicity') // 'toxicity' or 'timestamp'

  useEffect(() => {
    loadFeed()
  }, [])

  const loadFeed = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/feed`)
      setFeed(response.data)
    } catch (error) {
      console.error('Error loading feed:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAccept = async (postId, commentId) => {
    try {
      await axios.post(`${API_URL}/api/comment/accept`, {
        post_id: postId,
        comment_id: commentId
      })
      loadFeed()
    } catch (error) {
      console.error('Error accepting comment:', error)
    }
  }

  const handleDelete = async (postId, commentId) => {
    try {
      await axios.post(`${API_URL}/api/comment/delete`, {
        post_id: postId,
        comment_id: commentId
      })
      loadFeed()
    } catch (error) {
      console.error('Error deleting comment:', error)
    }
  }

  // Get all comments from all posts
  const allComments = feed.flatMap((post) =>
    (post.comments || []).map((comment) => ({
      ...comment,
      postId: post.id,
      postCaption: post.caption
    }))
  )

  // Sort comments
  const sortedComments = [...allComments].sort((a, b) => {
    if (sortBy === 'toxicity') {
      return (b.toxicity_score || 0) - (a.toxicity_score || 0)
    } else {
      return new Date(b.timestamp) - new Date(a.timestamp)
    }
  })

  if (loading) {
    return <div className="text-center py-8">Loading admin panel...</div>
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Admin Moderation Panel</h2>
        <div className="flex items-center gap-4">
          <label className="text-sm text-gray-600">Sort by:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="toxicity">Toxicity (High to Low)</option>
            <option value="timestamp">Timestamp (Newest First)</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Comment
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Toxicity Score
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Post
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedComments.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-4 py-8 text-center text-gray-500">
                  No comments to moderate
                </td>
              </tr>
            ) : (
              sortedComments.map((comment) => (
                <tr key={comment.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900 max-w-md">
                    {comment.text}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {comment.username || 'user'}
                  </td>
                  <td className="px-4 py-3">
                    <ToxicityBadge score={comment.toxicity_score || 0} />
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">
                    {comment.postCaption || 'N/A'}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleAccept(comment.postId, comment.id)}
                        className="px-3 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600"
                      >
                        ACCEPT
                      </button>
                      <button
                        onClick={() => handleDelete(comment.postId, comment.id)}
                        className="px-3 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600"
                      >
                        DELETE
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        Total comments: {sortedComments.length}
      </div>
    </div>
  )
}

export default AdminPanel

