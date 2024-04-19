import numpy as np
class AES128_Enc:
  SBox=bytearray([
      99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
      202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
      183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
      4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
      9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
      83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
      208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
      81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
      205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
      96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
      224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
      231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
      186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
      112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
      225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
      140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22])

  def _process_block_key(text,key):
      #Add padding bits and convert to hexadecimal integer for each of the key and text block in case they're strings:
      if isinstance(text,str):
            text=text.rjust(16,'0')
      text=bytearray.fromhex(text)
      if isinstance(key,str):
        #In case of invalid key where the number of nibbles per key string should be exactly 32 nibbles:
        if(len(key)!=32):
          print ('Invalid Key Length Please Enter a Valid 128 Bit Key!')
          #Exist Status for key
          key=None
        else:
          key=bytearray.fromhex(key)
      #Return tupple of textblock and key:
      return text,key


  def Block2array(text, key):
    # Preprocess text and key
      text, key = AES128_Enc._process_block_key(text, key)

      # Create a 16-byte grid from text block. Type is bytes.
      byte_grid = [bytes(text[i:i + 4]) for i in range(0, 16, 4)]

      # Check if the key is invalid, if so exit.
      if key is None:
          return byte_grid, 0

      # Create a list of 4-word columns from the key. Type is bytes.
      M_Key_Arr = [bytes(key[i:i + 4]) for i in range(0, 16, 4)]

      # Return the byte grid and the list of bytes representing the key
      return byte_grid, M_Key_Arr



  def KeyExpansion(M_Key_Arr):
    # First Rcon value
    Rcon_Arr = [0x1]
    Rcon_Bytes = bytes(0x1)

    # Generate Rcon values
    for i in range(9):
        Rcon_Arr.append(Rcon_Arr[i] * 2 if Rcon_Arr[i] * 2 < 256 else ((Rcon_Arr[i] * 2) ^ (0b11011)) & 0xFF)
        Rcon_Bytes += bytes(Rcon_Arr[i + 1])

    # Initialize Key_Exp with the initial key
    Key_Exp = []
    Key_Exp.append(M_Key_Arr)

    # Perform key expansion for 10 rounds
    for i in range(10):
        Wk = []
        # Generate the first word of the new round key
        for j in range(4):
            if j == 0:
                # Circular shift and apply SBox to the first word
                first_word = Key_Exp[i][3]
                first_word = first_word[1:] + first_word[:1]
                first_word = bytes(AES128_Enc.SBox[first_word[i]] for i in range(4))
                first_byte = first_word[0] ^ Rcon_Arr[i]
                first_byte = first_byte.to_bytes(1, 'big')
                first_word = first_byte + first_word[1:]
                last_word = first_word
            else:
                last_word = Wk[j - 1]
            # XOR the precedent word of the same position with the last word and append to word list
            prec_word = Key_Exp[i][j]
            xor = bytes(b1 ^ b2 for b1, b2 in zip(last_word, prec_word))
            Wk.append(xor)
        # Add round key to Key_Exp
        Key_Exp.append(Wk)

    return Key_Exp


  def Sub_Bytes(byte_grid):
    state_sub=[]
    #Substitute 4 bytes by a byte each from Sbox for each word in the state grid
    for list_bytes in byte_grid:
      state_sub.append(bytes(AES128_Enc.SBox [list_bytes[i]] for i in range(4)))
    return state_sub

  def Shft_Func(byt):
    #Each of these column variables have predefined byte positions from the original state array where a byte is rotated depending on the row number
    c0=byt[0][:1] + byt[1][1:2] + byt[2][2:3] + byt[3][3:]
    c1=byt[1][:1] + byt[2][1:2] + byt[3][2:3] + byt[0][3:]
    c2=byt[2][:1] + byt[3][1:2] + byt[0][2:3] + byt[1][3:]
    c3=byt[3][:1] + byt[0][1:2] + byt[1][2:3] + byt[2][3:]
    rot_state=[c0,c1,c2,c3]
    return rot_state


  def FieldMult(stat_byte, cons):
      if cons == 1:
          return stat_byte
      # Left-shift the byte by 1
      shft_byte = stat_byte << 1

      # Is the new length 9 bits?
      if (shft_byte & 0x100) != 0:
          # If yes, XOR with the AES irreducible polynomial (0x1B)
          shft_byte = (shft_byte ^ 0x1B) & 0xFF

      # If the constant is 2 return the shifted byte
      if cons == 2:
          return shft_byte
      else:
          # This involves XORing the result with the original value
          return shft_byte ^ stat_byte



  def MixColumn(state):
      #First row for the mix matrix (4x4 Array of constants)
      mix_mat = [[2,3,1,1]]
      #Add the remaining rows by rotating the first row to the right by the row number's amount
      mix_mat+=[mix_mat[0][4-i:]+mix_mat[0][:4-i] for i in range(1,4)]
      #Initialize the results Array
      byt_list=[]
      for i in range(4):
          #New_state is the temporary bytearray object that will contain a list of 4 bytearray objects (4 columns)
          New_state=bytearray()
          for j in range(4):
              #Perform Galois Field Multiplication for each column value then XOR the values to get the corresponding byte value for each element (repeat 4 times for the entire column)
              New_state+= (AES128_Enc.FieldMult(state[i][0], mix_mat[j][0]) ^
                  AES128_Enc.FieldMult(state[i][1], mix_mat[j][1]) ^
                  AES128_Enc.FieldMult(state[i][2], mix_mat[j][2]) ^
                  AES128_Enc.FieldMult(state[i][3], mix_mat[j][3])).to_bytes(1,'big')
          #Add the column bytearray result to the bytes' list
          byt_list.append(New_state)
      return byt_list




  def AddRoundKey(State_Arr,Rnd_Key):
    #Perform Byte-wise XOR operation between the state array and the current Round Key Array (Both 4x4 Arrays)
    State=[bytes(b1 ^ b2 for b1,b2 in zip(State_Arr[i],Rnd_Key[i])) for i in range(4)]
    return State

  def Encrypt(text,key):
    cipher=''
    #Preprocess Text and Key Blocks
    Text_Arr,Master_Arr=AES128_Enc.Block2array(text,key)
    #Invalid Key exit status (when Key is None)
    if(Master_Arr ==0):
      return 0
    #Generate Key Schedule
    Key_Sched=AES128_Enc.KeyExpansion(Master_Arr)
    #Initial Text-Key XOR
    state=AES128_Enc.AddRoundKey(Text_Arr,Key_Sched[0])
    #Round 1-10 uses 4 steps
    for round in range(1,10):
      state=AES128_Enc.Sub_Bytes(state)
      state=AES128_Enc.Shft_Func(state)
      state=AES128_Enc.MixColumn(state)
      state=AES128_Enc.AddRoundKey(state,Key_Sched[round])
    #Last Round uses 3 steps
    state=AES128_Enc.Sub_Bytes(state)
    state=AES128_Enc.Shft_Func(state)
    state=AES128_Enc.AddRoundKey(state,Key_Sched[10])
    #Proper hexadecimal formatting to avoid truncating leading zeroes, and reconstruction of the full cipher from the bytearray
    cip=''.join( format(element,'02x')  for row in state for element in row)
    return cip

  def Vector_Testing(test_vector):
      ind=0
      for key,values in test_vector.items():

        print('Encryption process for Test Vector #'+key+':\n'+
                'Text:'+values['TextBlock']+
                '\nKey: '+values['Key'])
        Cipher=AES128_Enc.Encrypt(values['TextBlock'],values['Key'])
        if(len(values['Key']) !=32):
          print('Exiting.......')
          return 0
        if(values['Cipher']==Cipher):
          print('Successful! \nwith cipher output: '+Cipher+
              '\n--------------------------------------------------' )
          ind+=1
        else:
          print('Cipher for Test Vector #'+str(ind)+' Is Incorrect. \nExiting....\n--------------------------------------------------' )
          return 0
      print('Encryption Successful, All '+str(ind)+' Block Ciphers Are Correct!')
      print('Exiting.......')
      print('\n--------------------------------------------------' )

Test_Vectors={'1' :{'TextBlock':'6bc1bee22e409f96e93d7e117393172a' ,'Key':'2b7e151628aed2a6abf7158809cf4f3c', 'Cipher': '3ad77bb40d7a3660a89ecaf32466ef97'},
              '2' :{'TextBlock':'ae2d8a571e03ac9c9eb76fac45af8e51' ,'Key':'2b7e151628aed2a6abf7158809cf4f3c', 'Cipher': 'f5d3d58503b9699de785895a96fdbaaf'},
              '3' :{'TextBlock':'30c81c46a35ce411e5fbc1191a0a52ef' ,'Key':'2b7e151628aed2a6abf7158809cf4f3c', 'Cipher': '43b1cd7f598ece23881b00e3ed030688'}
             }
AES128_Enc.Vector_Testing(Test_Vectors)

print('Encrypting a Block individually: ')
Master='0f1571c947d9e8590cb7add6af7f6798'
text=  '0123456789abcdeffedcba9876543210'
cipher=AES128_Enc.Encrypt(text,Master)
print(cipher)