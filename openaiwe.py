

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted

)


prompt= """
You are a translator of English to Spanish. You will recieve a text in English, sometimes with a term marked between the XML tag <br> and </br>. Then you translate the text to Spanish maintaining the XML tags <br> and </br> between the term. Some examples:
Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
Output: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de <br>computación móvil</br>."
Input: "Where have all the <br>PC makers</br> gone?".
Output: "¿Dónde se han ido todos los <br>fabricantes de PC</br>?".
Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail".
Output: "El papel del enredo cuántico del <br>estado inicial</br> se discute en detalle".
Input: "It often exploits an <br>optical diffusion model-based image reconstruction algorithm</br> to estimate spatial property values from measurements of the light flux at the surface of the tissue."
Output: "A menudo se utiliza un <br>algoritmo de reconstrucción de imágenes basado en un modelo de difusión óptica</br> para estimar los valores de propiedades espaciales a partir de medidas de la flujo de luz en la superficie del tejido."
"""
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  temperature=0,
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": "Input: \"A conferences impact on <br>undergraduate female students</br> In September of 2000, the 3rd Grace Hopper Celebration of Women in Computing was held in Cape Cod, Massachusetts.\""}
  ]
)
print(completion)
