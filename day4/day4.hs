import Data.List (dropWhileEnd)
import Data.List.Split
import Numeric (readHex)
import qualified Data.Set as S
import qualified Data.Map.Strict as M hiding (map)
import Debug.Trace (trace)

emptyLine :: String
emptyLine = "\n\n"

requiredKeys :: S.Set [Char]
requiredKeys = S.fromList $ splitOn " " "byr iyr eyr hgt hcl ecl pid"

allKeys :: S.Set [Char]
allKeys = S.fromList $ splitOn " " "byr iyr eyr hgt hcl ecl pid cid"

tuplify :: [a] -> (a, a)
tuplify [x,y] = (x,y)

isInRange :: Ord a => a -> a -> a -> Bool
isInRange lower upper x = lower <= x && x <= upper

(<?) :: Ord a => a -> (a,a) -> Bool
(<?) = flip (uncurry isInRange)
 
parsePassports :: [Char] -> [M.Map [Char] [Char]]
parsePassports = map (M.fromList . map (tuplify . splitOn ":") . splitOneOf " \n") . splitOn emptyLine . dropWhileEnd (=='\n')

validateYear :: Int ->  Integer -> Integer -> String -> Bool
validateYear l min max b = (length b == l) && ((read b::Integer) <? (min, max))

isInteger :: String -> Bool
isInteger s = case reads s :: [(Integer, String)] of
    [(_, "")] -> True
    _         -> False

validateHeight :: String -> Bool
validateHeight h = case reads h :: [(Integer, String)] of
    [(ht, unit)] -> case unit of
                      "cm" -> (<?) ht (150, 193)
                      "in" -> (<?) ht ( 59,  76)
                      _    -> False
    _  -> False


validateColor :: String -> Bool
validateColor (p:cs) = case p of
    '#' -> case readHex cs :: [(Integer, String)] of
        [(_, "")] -> True
        _         -> False
    _   -> False

solution1 x = (requiredKeys == M.keysSet x) || (allKeys == M.keysSet x)

solution2 x = 
                 validateYear 4 1920 2002 ((M.!) x "byr")
              && validateYear 4 2010 2020 ((M.!) x "iyr")
              && validateYear 4 2020 2030 ((M.!) x "eyr")
              && validateHeight ((M.!) x "hgt")
              && validateColor ((M.!) x "hcl")
              && (M.!) x "ecl" `elem` ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
              && length ((M.!) x "pid") == 9 && isInteger ((M.!) x "pid")
              

main = do
    a <- readFile "input4.real"
    let passports = parsePassports a
    putStr "Solution 1: " 
    print $ length $ filter solution1 passports
    putStr "Solution 2: " 
    print $ length $ filter solution2 $ filter solution1 passports
