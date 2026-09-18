import io
import math
import wave
from typing import Optional

import pygame


class MusicPlayer:
    """Generate and play a small looping chiptune without external assets."""

    def __init__(self) -> None:
        self._sound: Optional[pygame.mixer.Sound] = None
        self._channel: Optional[pygame.mixer.Channel] = None

    def start(self) -> None:
        if not pygame.mixer.get_init():
            return
        try:
            self._sound = pygame.mixer.Sound(file=io.BytesIO(self._make_song()))
            self._sound.set_volume(0.16)
            self._channel = self._sound.play(loops=-1)
        except pygame.error:
            self._sound = None
            self._channel = None

    def stop(self) -> None:
        if self._channel is not None:
            self._channel.stop()
        self._channel = None
        self._sound = None

    @staticmethod
    def _make_song() -> bytes:
        sample_rate = 22050
        beat_length = 0.25
        step_count = 32
        melody = (
            659, 659, 784, 880, 784, 659, 523, None,
            587, 587, 698, 784, 698, 587, 440, None,
            523, 523, 659, 784, 659, 523, 392, None,
            440, 523, 587, 659, 587, 523, 440, None,
        )
        bass = (
            131, None, 131, None, 98, None, 98, None,
            147, None, 147, None, 110, None, 110, None,
            131, None, 131, None, 98, None, 98, None,
            110, None, 110, None, 87, None, 87, None,
        )
        samples = bytearray()
        step_samples = int(sample_rate * beat_length)
        for step in range(step_count):
            melody_frequency = melody[step]
            bass_frequency = bass[step]
            for index in range(step_samples):
                time = index / sample_rate
                progress = index / step_samples
                fade = min(1.0, index / 180.0, (step_samples - index) / 700.0)
                value = 0.0

                if melody_frequency is not None:
                    melody_wave = 1.0 if math.sin(2 * math.pi * melody_frequency * time) >= 0 else -1.0
                    value += 0.34 * melody_wave * fade
                if bass_frequency is not None:
                    bass_wave = math.sin(2 * math.pi * bass_frequency * time)
                    value += 0.22 * bass_wave * fade

                # Kick on beats and a short noise-like snare on the off-beats.
                if step % 4 == 0 and progress < 0.22:
                    kick_fade = (1.0 - progress / 0.22) ** 2
                    value += 0.22 * math.sin(2 * math.pi * (105 - 55 * progress) * time) * kick_fade
                if step % 4 == 2 and progress < 0.12:
                    snare_fade = 1.0 - progress / 0.12
                    noise = math.sin(index * 17.31) * math.sin(index * 3.17)
                    value += 0.12 * noise * snare_fade

                value = max(-0.85, min(0.85, value))
                samples.append(int(128 + 127 * value))

        output = io.BytesIO()
        with wave.open(output, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(1)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(samples)
        return output.getvalue()
