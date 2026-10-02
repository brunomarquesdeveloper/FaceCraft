export async function requestCamera(): Promise<MediaStream> {
  if (!navigator.mediaDevices?.getUserMedia) {
    throw new Error('A câmera não é suportada neste navegador.')
  }

  return await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false
  })
}