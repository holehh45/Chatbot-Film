
import re


class IntentRecognizer:
	def recognize(self, text):
		text = text.lower().strip()

		# ======================
		# GREETING
		# ======================

		if re.search(
			r"\b(halo|hai|hello|hi)\b",
			text
		):
			return (
				"greeting",
				None
			)

		# ======================
		# THANKS
		# ======================

		if re.search(
			r"(terima kasih|makasih|thanks)",
			text
		):
			return (
				"thanks",
				None
			)

		# ======================
		# FOLLOW UP QUESTIONS
		# ======================

		if re.search(
			r"(ratingnya|berapa rating)",
			text
		):
			return (
				"rating_question",
				None
			)

		if re.search(
			r"(genrenya|genre apa)",
			text
		):
			return (
				"genre_question",
				None
			)

		if re.search(
			r"(tahun berapa|kapan rilis|rilis kapan)",
			text
		):
			return (
				"year_question",
				None
			)

		if re.search(
			r"(film serupa|film mirip|mirip|rekomendasi serupa)",
			text
		):
			return (
				"similar_movie",
				None
			)

		# ======================
		# MOVIE NUMBER
		# film 1
		# nomor 2
		# ======================

		number_match = re.search(
			r"(film|nomor)\s*(\d+)",
			text
		)

		if number_match:

			number = int(
				number_match.group(2)
			)

			return (
				"movie_number",
				number
			)

		# ======================
		# YANG PERTAMA
		# ======================

		if "yang pertama" in text:
			return (
				"movie_number",
				1
			)

		if "yang kedua" in text:
			return (
				"movie_number",
				2
			)

		if "yang ketiga" in text:
			return (
				"movie_number",
				3
			)

		if "yang keempat" in text:
			return (
				"movie_number",
				4
			)

		# ======================
		# RECOMMENDATION
		# ======================

		genre_match = re.search(
			r"(action|sci-fi|animation|drama|comedy|horror|romance)",
			text
		)

		if genre_match:

			genre = genre_match.group(1)

			if re.search(
				r"(rekomendasi|sarankan|film bagus|ingin film|suka genre|film genre)",
				text
			):

				return (
					"recommendation",
					genre
				)

		# ======================
		# DETAIL
		# detail interstellar
		# info titanic
		# ======================

		detail_match = re.search(
			r"(detail|info|informasi)\s+(.+)",
			text
		)

		if detail_match:

			title = (
				detail_match.group(2)
				.strip()
			)

			return (
				"detail",
				title
			)

		# ======================
		# SEARCH
		# cari film titanic
		# ======================

		search_match = re.search(
			r"cari film\s+(.+)",
			text
		)

		if search_match:

			title = (
				search_match.group(1)
				.strip()
			)

			return (
				"detail",
				title
			)

		# ======================
		# BACK
		# ======================

		if re.search(
			r"(menu|kembali|home)",
			text
		):
			return (
				"back",
				None
			)

		# ======================
		# UNKNOWN
		# ======================

		return (
			"unknown",
			None
		)


