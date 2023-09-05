"""
    Gather all full pipelines

"""
import nipype.interfaces.utility as niu
import nipype.pipeline.engine as pe


from nipype.interfaces.niftyreg.regutils import RegResample


def pad_skull_petra_outputs(params, main_workflow, segment_pnh_pipe,
                            skull_petra_pipe):

    # output node
    outputnode_native = pe.Node(
        niu.IdentityInterface(
            fields=["native_petra_skull_mask",
                    "native_robustpetra_skull_mask",
                    "native_petra_head_mask"]),
        name='outputnode_native')

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():
            pass
        else:
            print("Using reg_aladin transfo to pad skull_mask back")

            pad_petra_skull_mask = pe.Node(RegResample(inter_val="NN"),
                                           name="pad_petra_skull_mask")

            main_workflow.connect(
                skull_petra_pipe, "outputnode.petra_skull_mask",
                pad_petra_skull_mask, "flo_file")

            main_workflow.connect(
                segment_pnh_pipe, "outputnode.native_T1",
                pad_petra_skull_mask, "ref_file")

            main_workflow.connect(
                segment_pnh_pipe, "outputnode.cropped_to_native_trans",
                pad_petra_skull_mask, "trans_file")

            main_workflow.connect(
                pad_petra_skull_mask, "out_file",
                outputnode_native, "native_petra_skull_mask")

            print("Using reg_aladin transfo \
                to pad robustpetra_skull_mask back")

            print("Using reg_aladin transfo to pad head_mask back")

            pad_petra_head_mask = pe.Node(RegResample(inter_val="NN"),
                                          name="pad_petra_head_mask")

            main_workflow.connect(skull_petra_pipe,
                                  "outputnode.petra_head_mask",
                                  pad_petra_head_mask, "flo_file")

            main_workflow.connect(segment_pnh_pipe,
                                  "outputnode.native_T1",
                                  pad_petra_head_mask, "ref_file")

            main_workflow.connect(segment_pnh_pipe,
                                  "outputnode.cropped_to_native_trans",
                                  pad_petra_head_mask, "trans_file")

            main_workflow.connect(pad_petra_head_mask, "out_file",
                                  outputnode_native, "native_petra_head_mask")

            if "petra_skull_fov" in params["skull_petra_pipe"]:
                pad_robustpetra_skull_mask = pe.Node(
                    RegResample(inter_val="NN"),
                    name="pad_robustpetra_skull_mask")

                main_workflow.connect(
                    skull_petra_pipe,
                    "outputnode.robustpetra_skull_mask",
                    pad_robustpetra_skull_mask, "flo_file")

                main_workflow.connect(
                    segment_pnh_pipe, "outputnode.native_T1",
                    pad_robustpetra_skull_mask, "ref_file")

                main_workflow.connect(
                    segment_pnh_pipe,
                    "outputnode.cropped_to_native_trans",
                    pad_robustpetra_skull_mask, "trans_file")

                main_workflow.connect(
                    pad_robustpetra_skull_mask, "out_file",
                    outputnode_native, "native_robustpetra_skull_mask")
