import { useState, useEffect } from 'react'
import PostCard from './PostCard'
import Composer from './Composer'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function Feed() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFeed()
  }, [])

  const loadFeed = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/feed`)
      setPosts(response.data)
    } catch (error) {
      console.error('Error loading feed:', error)
      // Fallback to sample data if API fails
      setPosts([])
    } finally {
      setLoading(false)
    }
  }

  const handleCommentAdd = async (postId, text) => {
    try {
      await axios.post(`${API_URL}/api/comment/add`, {
        post_id: postId,
        text: text,
        username: 'user'
      })
      loadFeed() // Reload feed
    } catch (error) {
      console.error('Error adding comment:', error)
    }
  }

  const handleCommentAccept = async (postId, commentId) => {
    try {
      await axios.post(`${API_URL}/api/comment/accept`, {
        post_id: postId,
        comment_id: commentId
      })
      loadFeed() // Reload feed
    } catch (error) {
      console.error('Error accepting comment:', error)
    }
  }

  const handleCommentDelete = async (postId, commentId) => {
    try {
      await axios.post(`${API_URL}/api/comment/delete`, {
        post_id: postId,
        comment_id: commentId
      })
      loadFeed() // Reload feed
    } catch (error) {
      console.error('Error deleting comment:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading feed...</div>
  }

  return (
    <div className="space-y-6">
      <Composer onPostCreated={loadFeed} />
      {posts.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No posts yet. Create your first post!
        </div>
      ) : (
        posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onCommentAdd={handleCommentAdd}
            onCommentAccept={handleCommentAccept}
            onCommentDelete={handleCommentDelete}
          />
        ))
      )}
    </div>
  )
}

export default Feed

