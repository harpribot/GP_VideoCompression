from gaussian_process.compressor import Compressor

compressor = Compressor('frames_original/frame_*')
compressor.load_frames()
compressor.set_compressed_total_frames(10)
compressor.fit(parallel =False)
compressor.predict()
compressor.store_produced_frames('frames_reconstructed')
