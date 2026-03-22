import CommentItem from './CommentItem'

function CommentList({ comments, postId, onAccept, onDelete }) {
  if (!comments || comments.length === 0) {
    return (
      <div className="px-4 py-2 text-sm text-gray-500">
        No comments yet. Be the first to comment!
      </div>
    )
  }

  return (
    <div className="px-4 py-2 space-y-2">
      {comments.map((comment) => (
        <CommentItem
          key={comment.id}
          comment={comment}
          postId={postId}
          onAccept={onAccept}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

export default CommentList

