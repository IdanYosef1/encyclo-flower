import { Input } from "@chakra-ui/react";
import AddImageButton from "components/Buttons/AddImageButton";
import PostQuestionButton from "components/Buttons/PostQuestionButton";
import ImageFromQuestion from "components/ImageFromQuestion/ImageFromQuestions";
import { nanoid } from "nanoid";
import { useSelector } from "react-redux";

interface Props {
  postQuestion: (e: React.FormEvent) => Promise<void>;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => Promise<void>;
  images: any;
  setImages: React.Dispatch<any>;
  questionsIds: string[];
  setQuestionsIds: React.Dispatch<React.SetStateAction<string[]>>;
}

const FormToCommunity = ({
  postQuestion,
  handleChange,
  images,
  setImages,
  questionsIds,
  setQuestionsIds,
}: Props) => {
  const store = useSelector((state: any) => state);
  return (
    <form
      onSubmit={postQuestion}
      className="flex flex-col justify-center items-center w-[100%] md:max-w-[52.7%] m-auto"
    >
      <div className="flex items-center justify-center my-5 ">
        <p className="font-bold text-secondary  border-b-4  border-b-primary mb-7 text-2xl w-[158px] text-center ">
          {store.isQuestion ? "שאלה לקהילה" : "שיתוף תצפית"}
        </p>
      </div>

      <Input
        className="srelative p-2 mb-8 max-w-[100%] min-h-[80px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 "
        placeholder="מהי שאלתך?"
        onBlur={handleChange}
        minLength={5}
        required
        style={{
          backgroundColor: "rgb(229 231 235)",
          paddingBottom: "50px",
          borderRadius: "25px",
        }}
      />
      <div className="flex flex-row gap-10 ml-auto flex-wrap">
        {Array.from(images).map((image, index) => {
          return (
            <ImageFromQuestion
              key={nanoid()}
              index={index}
              image={image}
              images={images}
              setImages={setImages}
            />
          );
        })}
      </div>
      <AddImageButton
        questionsIds={questionsIds}
        setQuestionsIds={setQuestionsIds}
      />
      <br />
      <PostQuestionButton />
    </form>
  );
};

export default FormToCommunity;
