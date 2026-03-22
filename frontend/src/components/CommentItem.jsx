import ToxicityBadge from './ToxicityBadge'

function CommentItem({ comment, postId, onAccept, onDelete }) {
  return (
    <div className="flex items-start justify-between gap-2 py-1">
      <div className="flex-1">
        <p className="text-sm">
          <span className="font-semibold">{comment.username || 'user'}</span>{' '}
          {comment.text}
        </p>
        {comment.accepted && (
          <span className="text-xs text-green-600">✓ Accepted</span>
        )}
      </div>
      <div className="flex items-center gap-2">
        <ToxicityBadge score={comment.toxicity_score || 0} />
        <div className="flex gap-1">
          <button
            onClick={() => onAccept(postId, comment.id)}
            className="px-2 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600"
            title="Accept comment"
          >
            ACCEPT
          </button>
          <button
            onClick={() => onDelete(postId, comment.id)}
            className="px-2 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600"
            title="Delete comment"
          >
            DELETE
          </button>
        </div>
      </div>
    </div>
  )
}

export default CommentItem

