import speech_recognition as sr

def main():

	sound = "Audios/Ojos_azules.wav"
	r = sr.Recognizer()

	with sr.AudioFile(sound) as source:
		r.adjust_for_ambient_noise(source)

		print("Convirtiendo audio a texto")

		audio = r.listen(source)

		try:
			text = r.recognize_google(audio)
			print("Preguntaste: {} \n".format(text))
	
		except Exception as e:
			print("Error: " + str(e))
		


if __name__ == "__main__":
	main()
