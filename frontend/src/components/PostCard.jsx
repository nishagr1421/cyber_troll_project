import { useState } from 'react'
import CommentList from './CommentList'
import CommentComposer from './CommentComposer'

function PostCard({ post, onCommentAdd, onCommentAccept, onCommentDelete }) {
  const [showComments, setShowComments] = useState(true)
  const [likes, setLikes] = useState(post.likes || 0)

  const handleLike = () => {
    setLikes(likes + 1)
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg mb-6">
      {/* Post Header */}
      <div className="flex items-center px-4 py-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
          {post.username?.[0]?.toUpperCase() || 'U'}
        </div>
        <div className="ml-3">
          <p className="font-semibold text-sm">{post.username || 'user'}</p>
        </div>
        <p className="ml-auto text-xs text-gray-500">
          {new Date(post.timestamp).toLocaleDateString()}
        </p>
      </div>

      {/* Post Image */}
      {post.image_url && (
        <img
          src={post.image_url}
          alt={post.caption}
          className="w-full object-cover"
          style={{ maxHeight: '600px' }}
        />
      )}

      {/* Image Toxicity Badge */}
      {post.image_toxicity_score !== undefined && (
        <div className="px-4 py-2 bg-gray-50 border-b border-gray-200">
          <span className="text-xs text-gray-600">Image Toxicity: </span>
          <span
            className={`text-xs font-semibold ${
              post.image_toxicity_score < 0.3
                ? 'text-green-600'
                : post.image_toxicity_score < 0.7
                ? 'text-yellow-600'
                : 'text-red-600'
            }`}
          >
            {(post.image_toxicity_score * 100).toFixed(1)}%
          </span>
        </div>
      )}

      {/* Actions */}
      <div className="px-4 py-2 flex items-center gap-4">
        <button
          onClick={handleLike}
          className="flex items-center gap-2 text-gray-700 hover:text-red-500"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
          <span className="text-sm font-semibold">{likes}</span>
        </button>
        <button
          onClick={() => setShowComments(!showComments)}
          className="flex items-center gap-2 text-gray-700"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
          <span className="text-sm">{post.comments?.length || 0}</span>
        </button>
      </div>

      {/* Caption */}
      <div className="px-4 pb-2">
        <p className="text-sm">
          <span className="font-semibold">{post.username || 'user'}</span>{' '}
          {post.caption}
        </p>
        {/* Caption Toxicity Badge */}
        {(post.text_toxicity_score !== undefined || post.fused_toxicity_score !== undefined) && (
          <div className="mt-2 text-xs">
            {post.text_toxicity_score !== undefined && (
              <span className="mr-3">
                <span className="text-gray-600">Text: </span>
                <span
                  className={`font-semibold ${
                    post.text_toxicity_score < 0.3
                      ? 'text-green-600'
                      : post.text_toxicity_score < 0.7
                      ? 'text-yellow-600'
                      : 'text-red-600'
                  }`}
                >
                  {(post.text_toxicity_score * 100).toFixed(1)}%
                </span>
              </span>
            )}
            {post.fused_toxicity_score !== undefined && (
              <span>
                <span className="text-gray-600">Overall: </span>
                <span
                  className={`font-semibold ${
                    post.fused_toxicity_score < 0.3
                      ? 'text-green-600'
                      : post.fused_toxicity_score < 0.7
                      ? 'text-yellow-600'
                      : 'text-red-600'
                  }`}
                >
                  {(post.fused_toxicity_score * 100).toFixed(1)}%
                </span>
              </span>
            )}
          </div>
        )}
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="border-t border-gray-200">
          <CommentList
            comments={post.comments || []}
            postId={post.id}
            onAccept={onCommentAccept}
            onDelete={onCommentDelete}
          />
          <CommentComposer
            postId={post.id}
            onCommentAdd={onCommentAdd}
          />
        </div>
      )}
    </div>
  )
}

export default PostCard

