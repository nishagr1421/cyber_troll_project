function ToxicityBadge({ score }) {
  const getColor = (score) => {
    if (score < 0.3) return 'bg-green-100 text-green-800'
    if (score < 0.7) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getLabel = (score) => {
    if (score < 0.3) return 'Low'
    if (score < 0.7) return 'Med'
    return 'High'
  }

  return (
    <span
      className={`px-2 py-1 rounded text-xs font-semibold ${getColor(score)}`}
      title={`Toxicity Score: ${(score * 100).toFixed(1)}%`}
    >
      {getLabel(score)} {(score * 100).toFixed(0)}%
    </span>
  )
}

export default ToxicityBadge

