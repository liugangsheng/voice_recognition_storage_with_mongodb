#!/usr/bin/python3
# coding=utf-8
'''
声音录制程序
包括：将声音获取并重新编码
'''
import wave

import pyaudio


class recode():
    def recode(self, CHUNK=44100, FORMAT=pyaudio.paInt16, CHANNELS=2, RATE=44100, RECORD_SECONDS=3,
               WAVE_OUTPUT_FILENAME="record.wav"):
        '''
        录音方法
        :param CHUNK: 缓冲区大小
        :param FORMAT: 采样大小
        :param CHANNELS:通道数
        :param RATE:采样率
        :param RECORD_SECONDS:录制时间
        :param WAVE_OUTPUT_FILENAME:输出文件路径
        :return:NULL
        '''

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print(WAVE_OUTPUT_FILENAME)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == '__main__':
    a = recode()
    a.recode(RECORD_SECONDS=10, WAVE_OUTPUT_FILENAME="record_hongzhaoyuan.wav")
