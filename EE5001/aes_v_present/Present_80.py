import re
class Pres80:
  #Create Substitution box list:
  Sbox= [12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2]
  #Create Permutation box list:
  PBox = [0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
          4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
          8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
          12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
  def _process_block_key(text,key):
    #Add padding bits and convert to hexadecimal integer for each of the key and text block in case they're strings:
    if isinstance(text,str):
        #Using regular expressions to check whether the text is a regular text or a hexadecimal string
        if(re.match(r'^[0-9a-fA-F]+$',text.replace('0x',''))):
          text= int((text),16)
        else:
          #Convert regular text (like words) to hexadecimal string and remove overhead:
          #Also limit the amount of text to 8 characters (8 bit for each):
          text=text[0:8].encode('utf8').hex().replace('0x','')
          temp=text.rjust(16,'0')
          print(temp)
          #Pad the block when necessary, useful when not using test vectors then convert back to integer hexadecimal:
          text=int(text.rjust(16,'0'),16)
    if isinstance(key,str):
      #In case of invalid key where the number of nibbles per key string should be exactly 20 nybbles:
      if(len(key.upper().replace('0X',''))!=20):
        print ('Invalid Key Length Please Enter a Valid 80 Bit Key!')
        #Exist Status for key
        return text,0
      else:
        key=int(key,16)
    #Return tupple of textblock and key:
    return text,key
  def generateRoundkeys(key):
          #Initialise Round key list:
          roundkeys = []
          #create the first 31 round keys:
          for i in range(1,32):
                  #Select only the leftmost 64 bits (conversion from 80 to 64 bits):
                  roundkeys.append(key >>16)
                  #Rotate key bits by 19 bits to the right :takes the rightmost 19 bits and shifts them to the left and shift the original leftmost 61 bits to the right by 19 bits:
                  key = ((key & 0x7FFFF) << 61) + (key >> 19)
                  #Find the 4 bit value by substituting the leftmost 4 bits of the key with their equivalent value in the Sbox, shift it back and add it to the original key:
                  key = (Pres80.Sbox[key >> 76] << 76)+(key & 0xFFFFFFFFFFFFFFFFFFF)
                  #XOR key with round number value on the bits 15 to 20 of each round key. i>0  and <32 (5 bits) to add diffusion:
                  key ^= i << 15
          #Create the post-whitening key from the initial
          roundkeys.append(key >>16)
          return roundkeys
  def sBoxLayer(state):
        #Replace each 4 bits at a time of the original state block from right to left with their respective values from the Sbox list (using the 4 bit value as an index):
        state =sum(Pres80.Sbox[( state >> (i*4)) & 0xF] << (i*4) for i in range(16))
        return state
  def p_Layer(state):
          #Perform bit permutation operation  64 times using the values in the permutation box:
          state = sum(((state >> i) & 1) << Pres80.PBox[i] for i in range(64))
          return state

  def Encrypt(textblock,key):
                #Initialise state value with plaintext block value:
                state,key=Pres80._process_block_key(textblock,key)
                if(key==0):
                  return 0
                # Generate 32 round keys for the encryption process (including post-whitening subkey):
                roundkeys= Pres80.generateRoundkeys(key)
                #Perform 31 round 3-tier Encryption:
                for i in range (31):
                        #Add Round Key to State Block By doing Bit-wise XOR operation
                        state ^=roundkeys[i]
                        #Substitute respective values of the state from the substitution box:
                        state = Pres80.sBoxLayer(state)
                        #Shift Bits around using the predefined permutation list:
                        state = Pres80.p_Layer(state)
                #Add post-whitening round key:
                ciphertext = state^roundkeys[-1]
                #Convert back to hexadecimal, remove overhead to make it more suitable for chaining cipher blocks and convert back to str for viewing
                return str(hex(ciphertext)).upper().replace('0X','')

  def Vector_Testing(test_vector):
    cor,incor=0,0
    for key,values in test_vector.items():
      Cipher=Pres80.Encrypt(values['TextBlock'],values['Key'])
      print('Encryption process for Test Vector #'+key+':\n'+
              'Text:'+values['TextBlock']+
              '\nKey: '+values['Key'])
      if(values['Cipher']==Cipher):
        print('Is successful \nwith cipher output: '+Cipher+
            '\n--------------------------------------------------' )
        cor+=1
      else:
        print('Is Incorrect \n--------------------------------------------------' )
        incor+=1
    print('Total Correct: '+str(cor))
    print('Total Incorrect: '+str(incor))


Test_Vectors={'1' :{'TextBlock':'0000000000000000','Key':'40000000000000000000', 'Cipher':'756B6E92393D8D9D'},
             '2' :{'TextBlock': '0000000000000000' ,'Key':'80000000000000000000','Cipher': 'B112D5AC163C07A9'},
             '3' :{'TextBlock': 'FFFFFFFFFFFFFFFF' ,'Key':'FFFFFFFFFFFFFFFFFFFF','Cipher': '3333DCD3213210D2'}}




Pres80.Vector_Testing(Test_Vectors)
