export default function ScoreBar({ score, have }) {
  return (
    <div className="w-40 md:w-56">
      <div className="score-track">
        <div
          className={have ? 'score-fill-have' : 'score-fill-gap'}
          style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
        />
      </div>
    </div>
  )
}
