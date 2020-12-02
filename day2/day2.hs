import Control.Applicative hiding ((<|>))
import Text.ParserCombinators.Parsec
import Text.ParserCombinators.Parsec.Number
import Data.List
import Data.Char
import Data.Either
import Data.Algebra.Boolean (xor)

inputGrammer = endBy line eol
eol = string "\n"

data PasswordWithPolicy = Policy Int Int Char String deriving (Show)

line = Policy <$> (decimal <* char '-')
              <*> (decimal <* spaces)
              <*> (letter  <* char ':')
              <*> (spaces  *> many1 letter)

parseInput :: String -> Either ParseError [PasswordWithPolicy]
parseInput = parse inputGrammer "" 

myRights :: Either ParseError [PasswordWithPolicy] -> [PasswordWithPolicy]
myRights (Right b) = b
myRights (Left _)  = [] 

part1 :: PasswordWithPolicy -> Bool
part1 (Policy minOcc maxOcc letter text) = isInRange minOcc maxOcc (calcOcc text)
    where isInRange lower upper x = lower <= x && x <= upper
          calcOcc text = length $ filter (== letter) text

part2 :: PasswordWithPolicy -> Bool
part2 (Policy pos1 pos2 letter text) = xor (charAtPosEquals text pos1 letter) 
                                           (charAtPosEquals text pos2 letter)
    where charAtPosEquals text pos letter = (text!!(pos-1)) == letter

main = do
    contents <- readFile "input2.real"
    print $ length $ filter part2 $ myRights $ parseInput contents
