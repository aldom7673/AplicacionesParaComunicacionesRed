import speech_recognition as sr


def main():
	r = sr.Recognizer()


	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)

		print("Di algo...")

		audio = r.listen(source)

		try:
			print("Dijiste: \n" + r.recognize_google(audio))
	
		except Exception as e:
			print("Error: " + str(e))

if __name__ == "__main__":
	main()
