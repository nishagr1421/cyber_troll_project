import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function Composer({ onPostCreated }) {
  const [caption, setCaption] = useState('')
  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [prediction, setPrediction] = useState(null)

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!caption.trim() && !image) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('caption', caption)
      formData.append('username', 'user')
      if (image) {
        formData.append('image', image)
      }

      // Create the post (which includes toxicity prediction)
      const createResponse = await axios.post(
        `${API_URL}/api/post/create`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )

      if (createResponse.data.success) {
        alert('Post created successfully!')
        
        // Reset form
        setCaption('')
        setImage(null)
        setImagePreview(null)
        setPrediction(null)
        
        // Reload feed
        if (onPostCreated) {
          onPostCreated()
        }
      }
    } catch (error) {
      console.error('Error creating post:', error)
      alert('Error creating post. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <h2 className="text-lg font-semibold mb-4">Create New Post</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            placeholder="Write a caption..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Image
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {imagePreview && (
            <img
              src={imagePreview}
              alt="Preview"
              className="mt-2 max-w-xs rounded-md"
            />
          )}
        </div>

        {prediction && (
          <div className="p-3 bg-gray-50 rounded-md text-sm">
            <p className="font-semibold mb-1">Toxicity Prediction:</p>
            <div className="space-y-1">
              <p>Text: {(prediction.text_score * 100).toFixed(1)}%</p>
              <p>Image: {(prediction.image_score * 100).toFixed(1)}%</p>
              <p className="font-semibold">
                Fused: {(prediction.fused_score * 100).toFixed(1)}%
              </p>
              {prediction.tokens_flagged && prediction.tokens_flagged.length > 0 && (
                <p className="text-xs text-gray-600">
                  Flagged tokens: {prediction.tokens_flagged.join(', ')}
                </p>
              )}
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={uploading || (!caption.trim() && !image)}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {uploading ? 'Uploading...' : 'Create Post'}
        </button>
      </form>
    </div>
  )
}

export default Composer

